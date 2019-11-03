const fs = require('fs');
const rp = require('request-promise');

// API keys stored here
const secrets = require('./secret-api.secret.json');

// Libraries for using Azure Text-analytics services
const CognitiveServicesCredentials = require("@azure/ms-rest-js");
const TextAnalyticsAPIClient = require("@azure/cognitiveservices-textanalytics");



async function polisenService(dateFilter = (new Date).setHours((new Date).getHours()-48)) {  
    const POLISEN_API_URL = "https://polisen.se/api/events";
    let policeEvents;


    await rp(POLISEN_API_URL).then(body => { // Gets the JSON data from the Police's API
        policeEvents = JSON.parse(body);
    }).catch(err => {
        console.error(err);
    })
    
    const filteredPoliceEvents = policeEvents.filter(event => { // Filters out old events - default is to take events from the latest 48 hours
        return new Date(event.datetime) > new Date(dateFilter);
    })
    
    let output = [];
    for(event of filteredPoliceEvents) {
        output.push(await buildJSONfromPoliceEvent(event));
    }
    fs.writeFileSync('../../data/policeOutput.json', JSON.stringify(output), 'utf8');
}

const getKeywordsFromAzure = (text) => {   
    return new Promise((resolve, reject) => {        
        const creds = new CognitiveServicesCredentials.ApiKeyCredentials({ inHeader: { 'Ocp-Apim-Subscription-Key': secrets.apiKey } });
        const client = new TextAnalyticsAPIClient.TextAnalyticsClient(creds, secrets.keyPhrasesEndpoint);
        const inputDocuments = {
            documents: [{
                language: "sv",
                id: "1", 
                text
            }]
        };
        
        const operation = client.sentiment({multiLanguageBatchInput: inputDocuments})    
        operation.then(result => {
            const keyWords = result.documents[0].keyPhrases.map(keyWord => {
                return {
                    keyWord,
                    hits: 1
                }
            })
            resolve(keyWords);
        })
        .catch(err => {
            console.error(err);
            reject(err);
        });        
    })
};

const buildJSONfromPoliceEvent = async (event) => {    
    // Build up keywords & query Microsoft Text API for additional keywords
    let keyWords = [];
    let azureKeyWords = await getKeywordsFromAzure(event.summary);
    keyWords.push({keyWord: event.type}); // Adds the Keyword from Police's API to our object.
    azureKeyWords.forEach(word => { // Appends also all the keywords extracted from Azure Text Analytics Service
        keyWords.push(word);
    });
    
    return jsonObject = {
        "information": {
            "title": event.name,
            "text": event.summary,
            "imgUrl": undefined,
            "orignalSource": event.url,
            "location": event.location ? event.location.gps : undefined
        },
        "keyWords": keyWords,
        "category": {
            "tag": "Polisen",
            "category": "Polishändelse"
        },
        "datetime": event.datetime
    };    
}
polisenService();