var self = this;

this.app = null;

this.data = {
    user: {
        is_authenticated: false,
        name: null
    },
    tabs: [],
    current_tab: 0
};

$(document).ready(function() {
    self.app = new Vue({
        el: "#app",
        data: self.data,
        methods: {
            openTab: function(index) {
                self.data.current_tab = index;

                var tabId = self.data.tabs[index].id;
                $("#page-area").html($("#" + tabId + "-template").html());
            }
        }
    });

    $("#page-area").html($("#unicafe-template").html());
});
