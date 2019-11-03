const fs = require('fs');
const path = require('path');

// Reads the JSON returned from http://api.krisinformation.se/v1/capmessage?format=json
// Saved it locally here in this project to avoid needing to download 13mb json each time...

function krisInfoService() {
    const krisinfoObject = JSON.parse(fs.readFileSync(path.join(__dirname, 'krisinfo.json')));
    let filterDate = "2019-10-29";
    let filteredObject = krisinfoObject.filter((entry) => {
        return new Date(entry.Sent) > new Date(filterDate);
    })
    console.log(filteredObject);



    console.log("Testing");

}

krisInfoService();