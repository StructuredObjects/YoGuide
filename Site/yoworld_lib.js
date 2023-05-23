const web = require("axios");

class Item 
{
    SetInfo(arr) 
    {
        if(!Array.isArray(arr)) return;
        if(arr.length == 5)
        {
            this.name = arr[0]; this.id = arr[1]; this.url = arr[2];
            this.price = arr[3]; this.update = arr[4];
        } else {
            this.name = ""; this.id = ""; this.url = "";
            this.price = ""; this.update = "";
        }
    }
}

class Yoworld
{
    static FindItems(query)
    {
        var found = [];
        var data;
        axios.get("https://api.yoworld.site/search?q=" + query)
        .then(resp => {
            data = resp;
        }).catch(err => {
            console.log("[ X ] yoworld_lib.js | An error was occured in FindItems()")
            return [];
        })

        if(!data.startsWith("[") && !data.endsWith("]")) return;

        if(!data.include("\n")) 
        {
            
        }
    }
}

console.log(Yoworld.FindItems());