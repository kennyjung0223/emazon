// Main JS file
let url = "http://localhost:5000";

const handleSearch = (event) => {
    if (event.key === "Enter") {
        let searchPhrase = event.target.value;

        let newUrl = url + `/search/${searchPhrase}`;

        window.location.href = newUrl;
    }
}