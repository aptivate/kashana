define([
    'jquery',
], function ($) {
    function createSet(list) {
        var set = {};
        $.each(list, function (i, el) {
            set[el] = true;
        });
        return set;
    }

    var CleanInputMixin = {
        keep_tags: ["b", "i", "a", "p", "br", "strong", "em"],

        processNode: function(node, keep, wrapper) {
            var nodes, clean_node, processed_node,
                node_name;

            switch (node.nodeType) {
                case 3: // Text node
                    return node.parentNode ? node.parentNode.removeChild(node) : node;
                case 1:
                    node_name = node.nodeName.toLowerCase();
                    if (keep[node_name] || wrapper) {
                        clean_node = document.createElement(node_name);
                        if (node_name === "a") { // Special case
                            $(clean_node).attr("href", $(node).attr("href"));
                        }
                    } else {
                        clean_node = document.createDocumentFragment();
                    }
                    nodes = node.childNodes;
                    while(nodes.length) {
                        processed_node = this.processNode(nodes[0], keep);
                        if (processed_node) {
                            clean_node.appendChild(processed_node);
                        }
                    }
                    // Remove old one to prevent infinite loop
                    if (node.parentNode) {
                        node.parentNode.removeChild(node);
                    }
                    return clean_node;
                default:
                    // Drop other elements (comments...)
                    node.parentNode.removeChild(node);
            }
        },

        cleanInput: function (dirty) {
            var $el = $("<div>"),
                keep = createSet(this.keep_tags),
                el;
            $el.html(dirty);  // If there was Javascript, it will get executed here!!
            el = this.processNode($el[0], keep, true);
            return el.innerHTML;
        }
    };

    return CleanInputMixin;
});
