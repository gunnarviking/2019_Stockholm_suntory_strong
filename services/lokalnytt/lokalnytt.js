const fs = require('fs');
const path = require('path');
const express = require('express');
// const request = require('request');
const request = require('request-promise');
const cheerio = require('cheerio');
const secrets = require('../polisen/secret-api.secret.json');
// Libraries for using Azure Text-analytics services
const CognitiveServicesCredentials = require("@azure/ms-rest-js");
const TextAnalyticsAPIClient = require("@azure/cognitiveservices-textanalytics");


const LOKALNYHETER_SVT_URL = [{location: "blekinge", url: "https://www.svt.se/nyheter/lokalt/blekinge/"},
{location: "dalarna", url: "https://www.svt.se/nyheter/lokalt/dalarna/"},
{location: "gavleborg", url: "https://www.svt.se/nyheter/lokalt/gavleborg/"},
{location: "halland", url: "https://www.svt.se/nyheter/lokalt/halland/"},
{location: "jamtland", url: "https://www.svt.se/nyheter/lokalt/jamtland/"},
{location: "jonkoping", url: "https://www.svt.se/nyheter/lokalt/jonkoping/"},
{location: "norrbotten", url: "https://www.svt.se/nyheter/lokalt/norrbotten/"},
{location: "skane", url: "https://www.svt.se/nyheter/lokalt/skane/"},
{location: "smaland", url: "https://www.svt.se/nyheter/lokalt/smaland/"},
{location: "sodertalje", url: "https://www.svt.se/nyheter/lokalt/sodertalje/"},
{location: "stockholm", url: "https://www.svt.se/nyheter/lokalt/stockholm/"},
{location: "helsingborg", url: "https://www.svt.se/nyheter/lokalt/helsingborg/"},
{location: "uppsala", url: "https://www.svt.se/nyheter/lokalt/uppsala/"},
{location: "varmland", url: "https://www.svt.se/nyheter/lokalt/varmland/"},
{location: "vasterbotten", url: "https://www.svt.se/nyheter/lokalt/vasterbotten/"},
{location: "vastmanland", url: "https://www.svt.se/nyheter/lokalt/vastmanland/"},
{location: "orebro", url: "https://www.svt.se/nyheter/lokalt/orebro/"},
{location: "ost", url: "https://www.svt.se/nyheter/lokalt/ost/"},
{location: "vasternorrland", url: "https://www.svt.se/nyheter/lokalt/vasternorrland/"},
{location: "vast", url: "https://www.svt.se/nyheter/lokalt/vast/"},
{location: "sormland", url: "https://www.svt.se/nyheter/lokalt/sormland/"}]




async function getOneLokalNyttSite(lokalnytt) {
    let localNewsObject = [];
    return new Promise((resolve, reject) => {
        request(lokalnytt.url, async (error, response, html) => {
            if(!error) {
                let $ = cheerio.load(html);
                
                for(let i = 0; i<10; i++) {
                    let title, text, originalSource;
                    title = $(`#news-main--${i}  .nyh_teaser__heading`).text();
                    text = $(`#news-main--${i}  .nyh_teaser__textcontent`).text()
                    originalSource = "https://www.svt.se" + $(`#news-main--${i} a`).attr('href');
                    if(! (title.length>0 && text.length > 0 && originalSource.length > 0)) continue; // if no content then continue
                    
                    console.log(`Title: ${title}`)
                    console.log(`Text: ${text}`)
                    console.log(`URL: ${originalSource}`)
                    
                    let articleHTML;
                    await request(originalSource, async(error, response, tempHTML) => {
                        articleHTML = tempHTML;
                    })
                    let $article = cheerio.load(articleHTML);
                    const timeElementSelector = '.Timestamp__root___3Lbrt time';
                    const datetime = $article(timeElementSelector).attr('datetime');
                    
                    const enhancedLocalNews = await buildJSONfromLocalNews({
                        title,
                        text,
                        location: lokalnytt.location,
                        originalSource,
                        datetime
                    });
                    localNewsObject.push(enhancedLocalNews);
                }
                console.log("1 SITE OBJECT: ", localNewsObject)
                resolve(localNewsObject);
            }
            reject();
        });
    })
}

async function scrapeLocalNews() {
    let localNewsObject = [];
    
    return new Promise(async (resolve, reject) => {                        
        for(lokalnytt of LOKALNYHETER_SVT_URL) {
            const lokalnyheterEntry = await getOneLokalNyttSite(lokalnytt);
            localNewsObject = localNewsObject.concat(lokalnyheterEntry);
        };
        console.log(localNewsObject);
        resolve(localNewsObject);
        
    });
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
        resolve([{keyWord:"",hits:1}])
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


const buildJSONfromLocalNews = async (localNews) => {    
    // Build up keywords & query Microsoft Text API for additional keywords
    let keyWords = [];
    let azureKeyWords = await getKeywordsFromAzure(localNews.title + " " +  localNews.text);
    azureKeyWords.forEach(word => { // Appends also all the keywords extracted from Azure Text Analytics Service
        keyWords.push(word);
    });
    
    return jsonObject = {
        information: {
            title: localNews.title,
            text:localNews.text,
            "imgUrl": undefined,
            orignalSource: localNews.originalSource,
            location: localNews.location
        },
        "keyWords": keyWords,
        "category": {
            "tag": "Lokalnytt",
            "category": "Nyheter"
        },
        datetime: localNews.datetime
    };    
}

let scraper = async () => {    
    const svtData = await scrapeLocalNews();
    fs.writeFileSync(path.join(__dirname, 'svtData.json'), JSON.stringify(svtData));
}

scraper();