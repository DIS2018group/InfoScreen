var self = this;

this.infoscreen = {};
this.infoscreen.data = {
    user: {
        is_authenticated: false,
        name: null
    },
    tabs: [],
    current_tab: null
};
this.infoscreen.tabs = [];

$(document).ready(function() {
    var infoscreen = self.infoscreen;

    infoscreen.app = new Vue({
        el: "#app",
        data: infoscreen.data,
        methods: {
            openTab: openTab
        }
    });

    // Update user status every 0.5s
    window.setInterval(function() {
        updateStatus();
    }, 500);

    openTab(0);
});

function openTab(index) {
    var infoscreen = self.infoscreen;

    // Deactivate current tab (if any)
    if (infoscreen.data.current_tab !== null) {
        infoscreen.tabs[infoscreen.data.current_tab].deactivate();
    }

    infoscreen.data.current_tab = index;

    // Activate the new tab
    var tabId = infoscreen.data.tabs[index].id;
    $("#page-area").html($("#" + tabId + "-template").html());
    self.infoscreen.tabs[index].activate();
}

function updateStatus() {
    $.ajax({
        dataType: "json",
        url: "/heartbeat/",
        success: function(data) {
            infoscreen.data.user = data.user;
        }
    });
}
