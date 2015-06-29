function validateBirthday(birthday) {

}

// save inputted name and birthday
function saveOptions() {
    var name = document.getElementById('name').value;
    var birthday = document.getElementById('birthday').value;
    var statusMessage = "Settings saved";
    if (validateBirthday(birthday)) {
        chrome.storage.sync.set({
            name: name,
            birthday: birthday
        }, function() {
            // Update status to let user know options were saved.
            
        });
    } 
    var status = document.getElementById('update_status');
    status.innerHTML = 'Settings saved';
}

// deletes a users saved name and birthday, clears inputs
function clearOptions() {
    chrome.storage.sync.set({
        name: '',
        birthday: ''
    }, function() {
        // Update status to let user know options were saved.
        var status = document.getElementById('update_status');
        status.innerHTML = 'Settings cleared';
        document.getElementById('name').value = '';
        document.getElementById('birthday').value = '';
    });
}

// restores a users name and birthday to populate inputs
function restoreOptions() {
    chrome.storage.sync.get({
        name: '',
        birthday: ''
    }, function(data) {
        document.getElementById('name').value = data.name;
        document.getElementById('birthday').value = data.birthday;
    });
}

// startup, event listeners
document.addEventListener('DOMContentLoaded', function() {
    // load saved name/birthday
    restoreOptions();
    // save name/birthday
    document.getElementById('update_btn').addEventListener('click', function(e){
        e.preventDefault();
        saveOptions();
    });
    // clear name/birthday
    document.getElementById('clear_btn').addEventListener('click', function(e){
        e.preventDefault();
        clearOptions();
    });
    // return to horoscope
    document.getElementById('return_link').addEventListener('click', function(e){
        e.preventDefault();
        chrome.tabs.getCurrent(function(tab){
            chrome.tabs.create({},function(){
                chrome.tabs.remove(tab.id);
            });
        });
    });
});