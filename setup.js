(function ($) {

    $(function(){
        window.collections = {};
        window.views = {};
        window.models = {};

        Backbone.couch_connector.config.db_name = "bb";
        Backbone.couch_connector.config.ddoc_name = "bb";
        Backbone.couch_connector.config.global_changes = true;
        Backbone.couch_connector.config.base_url = "http://couch.czub.us";
        //Backbone.couch_connector.config.base_url = "http://czub.us/couchdb/";
        //Backbone.couch_connector.config.base_url = "http://bb:5984/";
        //
        // set up some input field finding utility methods
        Backbone.View.prototype.getInput = function(sel) {
            return this.inputs.filter(sel);
        };
    });
})(jQuery);
