// Main JS file
let url = "http://localhost:5000";
let method;

const handleSearch = () => {
    if (event.key === "Enter") {
        let searchKeyword = event.target.value;
        
        let newUrl = `${url}/search/${searchKeyword}`;
        method = "GET";

        let xhttp = new XMLHttpRequest();
        xhttp.open(method, url, true);
        xhttp.send();
        xhttp.onload = function() {

        }
        
    }
    
    
}