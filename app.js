const net = require("net");
const fs = require('fs')
const shell = require('shelljs');
const url = require('url');
const convertXML = require('xml-js');
const parseString = require('xml2js').parseString;
const crypto = require('crypto')

function ScanNormal(data){
  var siteURL = data.siteURL;
  var siteHref = data.urlHref;
  var settings = data.settings;
  console.log('Running scan queue');
  return new Promise(function(resolve, reject) {
    let sessionKey = randomS(4);

    let file = {};
    file.screenshot = './tmp/'+sessionKey+'screen.png';
    file.lighthouseFR_Dir = './tmp/'+sessionKey+'dlp.json';
    file.requestInfo = './tmp/'+sessionKey+'ri.json';
    file.phishFinder = './tmp/'+sessionKey+'pf.json';

    silent = true;

    // let LighthouseFRParams = 'python3 ./lighthouseFR/lh2.py "'+siteHref+'" 0 -o '+file.lighthouseFR_Dir;
		// lighthouseFR is available at https://github.com/Frohrer/lighthouse2
    let SelpyParams = 'python3 ./selpy/run.py "'+siteHref+'" '+sessionKey+'screen.png';
    let RequestInfoParams = 'python3 ./requestInfo/requestInfo.py "'+siteHref+'" -o '+file.requestInfo;
    let PhishFinderParams = 'python3 ./phishFinder/phishFinder.py "'+siteHref+'" -o '+file.phishFinder;

    let scanstate = {};
    scanstate.timeout = 4; // x times 5 seconds is the timeout in seconds for the whole scan. Scans that take too long should be timed out.
    if (settings.lighthouseFR === true) {
      scanstate.lighthouseFR = false;
    } else {
      scanstate.lighthouseFR = true;
    }
    scanstate.screenshot = false;
    scanstate.requestInfo = false;
    scanstate.phishFinder = false;

    let result = {};

    if (scanstate.lighthouseFR === false) {
      shell.exec(LighthouseFRParams, {async:false,silent:silent}, function(code,stdout,stderr) {
        fs.readFile(file.lighthouseFR_Dir, 'utf8', function (err,data) {
          try {
            result.lighthouseFR = JSON.parse(data)
          } catch (e) {
            result.lighthouseFR = {}
            console.log(e);
          } finally {
            scanstate.lighthouseFR = true;
          }
        })
      })
    }
    if (scanstate.requestInfo === false) {
      shell.exec(RequestInfoParams, {async:false,silent:false}, function(code,stdout,stderr) {
        fs.readFile(file.requestInfo, 'utf8', function (err,data) {
          try {
            result.requestInfo = JSON.parse(data)
          } catch (e) {
            result.requestInfo = {}
            console.log(e);
          } finally {
            scanstate.requestInfo = true;
          }
        })
      })
    }
    if (scanstate.screenshot === false) {
      shell.exec(SelpyParams, {async:false,silent:silent}, function(code,stdout,stderr) {
        fs.readFile(file.screenshot, 'base64', function (err,data) {
          try {
            result.screenshot = data.replace(/^data:image\/png;base64,/, "");
          } catch (e) {
            result.screenshot = {}
            console.log(e);
          } finally {
            scanstate.screenshot = true;
          }
        })
      })
    }
    if (scanstate.phishFinder === false) {
      shell.exec(PhishFinderParams, {async:false,silent:silent}, function(code,stdout,stderr) {
        fs.readFile(file.phishFinder, 'utf8', function (err,data) {
          try {
            result.phishFinder = JSON.parse(data)
          } catch (e) {
            result.phishFinder = {}
            console.log(e);
          } finally {
            scanstate.phishFinder = true;
          }
        })
      })
    }
    resolveScans(scanstate).then((done) => {
      for (entry in file) {
        try {
          fs.unlinkSync(file[entry])
        } catch (e) {
          console.log(e);
        }
      }
      resolve(result)
    })
  })
}

resolveScans = function(scanstate){ //checks that all scan parameters are fulfilled
  console.log('checking state for ',scanstate);
  return new Promise((resolve,reject) => {
    var state = true;
    for (key in scanstate){
      if (scanstate[key] == false) {
        state = false;
      } else {
      }
    }
    if (state == true || scanstate.timeout == 0) {
      resolve(true)
    } else {
      setTimeout(function() {
        scanstate.timeout--;
        resolve(resolveScans(scanstate));
      }, 5000)
    }
  })
}

function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
}

// Create a simple server
var server = net.createServer(function (conn) {
    console.log("Server: Client connected");

    // If connection is closed
    conn.on("end", function() {
        console.log('Client disconnected');
    });
    conn.on("error", function(error) {
      console.log(error);
    })
    // Handle data from client
		// Data object looks like this:
		// data = {
		// 	siteURL: 'example.com',
		// 	urlHref: 'https://example.com/',
		// 	settings: {
		// 		lighthouseFR:false,
		// 	}
		// }
    conn.on("data", function(data) {
      data = JSON.parse(data);
      console.log(typeof(data));
      if (typeof(data) == 'object') {
        console.log(data);
          ScanNormal(data).then((results) => { //includes all other scans
            conn.write(
              JSON.stringify(
                  { response: 'success', scan:results }
              )
            );
            conn.end()
          })
      } else {
        conn.end()
      }
  });
})
server.listen(8080, "0.0.0.0", function () {
    console.log("Server: Listening");
});

function randomS(x) {
  return crypto.randomBytes(x).toString('hex')
}

function testScan(){
	data = {
		siteURL: 'example.com',
		urlHref: 'https://example.com/',
		settings: {
			lighthouseFR:false,
		}
	}
	ScanNormal(data).then((results) => {
		console.log(results);
		fs.writeFile('./example.json',JSON.stringify(results), (err) => {
      if (err) {
        console.log(err);
      } else {
        console.log('Test done.');
      }
		})
	})
}

testScan()
