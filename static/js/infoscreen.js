var self = this;

self.infoscreen = {};
self.infoscreen.data = {
    users: {},
    tabs: [],
    current_tab: 0
};
this.infoscreen.tab_components = [];

$(document).ready(function() {
    var infoscreen = self.infoscreen;

    infoscreen.app = new Vue({
        el: "#app",
        data: infoscreen.data,
        methods: {
            openTab: openTab,
            addTab: addTab,
            updateUserTimestamp: updateUserTimestamp
        }
    });

    // Update user status every 0.5s
    window.setInterval(function() {
        updateStatus();
    }, 500);

    openTab(0);
});

function addTab(id) {
    infoscreen.tab_components.push(window[id.toUpperCase()]);
    Vue.component(id, {
        template: "#" + id + "-template",
        // All tabs share the same state
        data: function() { return self.infoscreen.data }
    });
};

function openTab(index) {
    var infoscreen = self.infoscreen;

    // Deactivate current tab (if any)
    infoscreen.tab_components[infoscreen.data.current_tab].deactivate();

    infoscreen.data.current_tab = index;

    // Activate the new tab
    var tabId = infoscreen.data.tabs[index].id;
    self.infoscreen.tab_components[index].activate();
};

/*
 * Update user data with a new timestamp to make sure it is synchronized with
 * the database
 */
function updateUserTimestamp(authId) {
    infoscreen.data.users[authId]["data"]["timestamp"] = +new Date() / 1000.0;
}

function updateStatus() {
    var updateObject = {};

    Object.keys(infoscreen.data.users).forEach(function(key, index) {
        var user = infoscreen.data.users[key];

        updateObject[user["user_id"]] = user["data"];
    });

    $.ajax({
        data: {"update": JSON.stringify(updateObject)},
        method: "POST",
        dataType: "json",
        url: "/heartbeat/",
        success: function(data) {
            var loggedInUsers = Object.keys(data.users);
            loggedInUsers.forEach(function(key, index) {
                if (key in infoscreen.data.users) {
                    var localTimestamp = infoscreen.data.users[key]["data"]["timestamp"];
                    if (localTimestamp === undefined) {
                        localTimestamp = -1;
                    }
                } else {
                    localTimestamp = -1;
                }

                var remoteTimestamp = data.users[key]["data"]["timestamp"];
                if (remoteTimestamp === undefined) {
                    remoteTimestamp = -1;
                }

                // Only update user data if it's out-of-date
                if (localTimestamp <= remoteTimestamp) {
                    var userDataListener = {
                        get: function(obj, prop) {
                            obj["data"]["timestamp"] = +new Date() / 1000.0;
                            return obj[prop];
                        }
                    };

                    Vue.set(infoscreen.data.users, key, data.users[key]);
                }
            });

            // Remove users which are no longer logged in
            Object.keys(infoscreen.data.users).forEach(function(key, index) {
                if (loggedInUsers.indexOf(key) === -1) {
                    // Use Vue.delete to make sure Vue reacts to changes
                    Vue.delete(infoscreen.data.users, key);
                }
            });
        }
    });
}
