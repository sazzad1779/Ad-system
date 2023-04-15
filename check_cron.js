var cron = require('node-cron');
const axios = require("axios");
const {spawn} = require('child_process');
var count=0;
cron.schedule('*/10 * * * * *', async () => {
    console.log('running a task every 20 second');

    try {
        console.log(count);
        if(count===0){
            
            const response=await axios.get("http://128.199.176.47:8080/camera_status");

            if(response.status==200){
                 
                if(response.data.status=="ON"){
                        count=1;
                        console.log("RUNNING PYTHON SCRIPT");
                        const pythonProcess = spawn('python3', ['main.py']);

                        pythonProcess.stdout.on('data', (data) => {
                        console.log(`stdout: ${data}`);
                        });

                        pythonProcess.stderr.on('data', (data) => {
                        console.error(`stderr: ${data}`);
                        });

                        pythonProcess.on('close', (code) => {
                        console.log(`child process exited with code ${code}`);
                        count=0;
                        });
                }
            }

        }

        
    
    } catch (error) {
  
      console.log(error.message);
      
    }

  
  });