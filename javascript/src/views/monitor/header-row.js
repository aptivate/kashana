define([
    'views/generic/list',
], function (ListView) {
    var MonitorHeaderRowView = ListView.extend({
        tagName: 'tr',
        template_selector: '#monitor-header-row',
        unknownName: '(undefined)',

        // Think of this as a public static method; data-entry-row uses it too.
        firstMilestone: function(milestones){
            return milestones.first();
        },

        // Think of this as a public static method; data-entry-row uses it too.
        nextMilestone: function(milestones){
            return milestones.filter(function (milestone) {
                return new Date(milestone.get('date')).getTime() >= Date.now();
            })[0];
        },
        
        // Return the name of the first milestone (baseline) 
        // or undefined if not available
        getMilestoneName: function (selectMilestone) {
            var milestone = selectMilestone(Aptivate.logframe.milestones);
            return milestone ? milestone.get('name') : this.unknownName;
        },

        listItems: function () {
            return this.collection.slice(-3); // TODO: use settings
        },

        
        getTemplateData: function () {
            var data = ListView.prototype.getTemplateData.apply(this, arguments);
            data.baseline = this.getMilestoneName(this.firstMilestone);
            data.milestone = this.getMilestoneName(this.nextMilestone);
            return data;
        },
    });

    return MonitorHeaderRowView;
});
