define([
    'views/base_view',
    'utils/display-date',
], function (BaseView, displayDate){

    var StatusHistoryView = BaseView.extend({
        tagName: 'tr',
        template_selector: '#activity-statushistory',

        getTemplateData: function (data) {
            var code, user;
            if (data.code) {
                code = _.where(Aptivate.data.statuscodes, {id: data.code});
                data.code_name = code.length ? code[0].name : "";
            }
            data.date = displayDate(data.date);
            if (data.user) {
                user = _.where(Aptivate.data.users,
                               {id: data.user});
                data.user_name = user.length ? user[0].name : "";
            }
            return data;
        }
    });

    return StatusHistoryView;
});
