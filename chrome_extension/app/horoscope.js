function generateHoroscope(now,birthday) {
    if (null === birthday) {
        birthday = new Date(now.getFullYear(), now.getMonth()-1, now.getDate());
    }
    console.log(birthday);
    return false;
    var seed = today.getTime() + birthday.getTime();
}

function loadHoroscope() {
    var now = new Date(); 
    chrome.storage.sync.get({
        horoscope: null,
        expires: null,
        birthday: null
    }, function(data) {
        if (null === data.expires || null === data.horoscope || data.expires <= now) {
            data.horoscope = generateHoroscope(now,data.birthday);
        }
        document.getElementById('text').innerHtml = data.horoscope;
    });
}

function loadUser() {
    chrome.storage.sync.get({
        name: null
    }, function(data) {
        if (null !== name) {

        }
        document.getElementById('title').innerHtml = data.name;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    loadUser();
    loadHoroscope();
    document.getElementById('options_link').addEventListener('click', function(e){
        e.preventDefault();
        chrome.extension.sendRequest({redirect: chrome.extension.getURL("/options/options.html")});
        window.location=chrome.extension.getURL("/options/options.html");
    });
});
