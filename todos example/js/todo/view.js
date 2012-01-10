(function ($) {

    $(function(){
        window.TodoView = Backbone.View.extend({
            tagName: "li",
            template: _.template($('#item-template').html()),
            events: {
                "click .check": "toggleDone",
                "dblclick div.todo-text": "edit",
                "click span.todo-destroy": "clear",
                "keypress .todo-input": "updateOnEnter"
            },
            initialize: function() {
                _.bindAll(this, 'render', 'remove');
                this.model.bind('change', this.render);
                this.model.bind('destroy', this.remove);
                this.model.bind('remove', this.remove);
            },
            render: function(){
                $(this.el).html(this.template(this.model.toJSON()));
                this.setText();
                return this;
            },
            setText: function() {
                var text = this.model.get('text');
                this.$('.todo-text').text(text);
                this.input = this.$('.todo-input');
                this.input.bind('blur', _.bind(this.close, this)).val(text);
            },
            toggleDone: function() {
                this.model.toggle();
            },
            edit: function() {
                $(this.el).addClass("editing");
                this.input.focus();
            },
            close: function() {
                this.model.save({text: this.input.val()});
                $(this.el).removeClass("editing");
            },
            updateOnEnter: function(e) {
                if (e.keyCode == 13) this.close();
            },
            remove: function() {
                $(this.el).remove();
            },
            clear: function() {
                this.model.destroy();
            },
        });
    });
})(jQuery);
