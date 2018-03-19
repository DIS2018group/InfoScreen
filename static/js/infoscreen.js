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
            addTab: addTab
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

function updateStatus() {
    $.ajax({
        dataType: "json",
        url: "/heartbeat/",
        success: function(data) {
            infoscreen.data.users = data.users;
        }
    });
}
