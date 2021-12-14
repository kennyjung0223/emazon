// Main JS file
let url = "";

const handleSearch = (event) => {
    if (event.key === "Enter") {
        let searchPhrase = event.target.value;

        let newUrl = url + `/search/${searchPhrase}`;

        window.location.href = newUrl;
    }
}

const addToCart = (itemName) => {
    let method = 'POST';
    let newUrl = url + '/';

    let item_details = {
        "name": itemName
    };

    let xhttp = new XMLHttpRequest();
    xhttp.open(method, newUrl, true);

    xhttp.send(item_details);

    xhttp.onload = function() {

    };
    
}