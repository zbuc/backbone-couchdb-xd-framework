(function ($) {

    $(function(){
        window.TodoList = Backbone.Collection.extend({
            model: Todo,
            url: "/todos",
            done: function() {
                return this.filter(function(todo){ return todo.get('done'); });
            },
            remaining: function() {
                return this.without.apply(this, this.done());
            },
            nextOrder: function() {
                if (!this.length) return 1;
                return this.last().get('order') + 1;
            },
            comparator: function(todo) {
                return todo.get('order');
            },
            db: {
                changes: true,
                filter : Backbone.couch_connector.config.ddoc_name + "/by_collection",
                view : "byCollection"
            }
        });

        window.Todos = new TodoList;
    });
})(jQuery);
