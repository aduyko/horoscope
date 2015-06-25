// save inputted name and birthday
function save_options() {
    var name = document.getElementById('name').value;
    var birthday = document.getElementById('birthday').value;
    chrome.storage.sync.set({
        name: name,
        birthday: birthday
    }, function() {
        // Update status to let user know options were saved.
        var status = document.getElementById('update_status');
        status.innerHTML = 'Settings saved';
    });
}

// deletes a users saved name and birthday, clears inputs
function clear_options() {
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
function restore_options() {
    chrome.storage.sync.get({
        name: '',
        birthday: ''
    }, function(user) {
        document.getElementById('name').value = user.name;
        document.getElementById('birthday').value = user.birthday;
    });
}

// startup, event listeners
document.addEventListener('DOMContentLoaded', function() {
    // load saved name/birthday
    restore_options();
    // save name/birthday
    document.getElementById('update_btn').addEventListener('click', function(e){
        e.preventDefault();
        save_options();
    });
    // clear name/birthday
    document.getElementById('clear_btn').addEventListener('click', function(e){
        e.preventDefault();
        clear_options();
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