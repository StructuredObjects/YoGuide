const fs = require("fs");

function Main() {
    var args = process.argv
    console.log(args)

    if(args.length == 3) {
        console.log(`[ X ] Error, Invalid arguments provided....\n${args[1]} ${args[2]}`)
    }
    console.log("here");
    
}

Main();