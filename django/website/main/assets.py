from django_assets import Bundle, register

# Main CSS

kashana_scss = Bundle('scss/kashana.scss',
                  filters='pyscss',
                  output='kashana/kashana.css',
                  depends='scss/**/*.scss')

pure_css = Bundle('css/pure.min.css')
pen_css = Bundle('css/pen.css')
ui_jq_css = Bundle('css/redmond/jquery-ui-1.11.4.custom.min.css')
jq_select_box_css = Bundle('css/select2/select2.min.css')
django_tables_css = Bundle('django_tables2/themes/paleblue/css/screen.css')

css_all = Bundle(pure_css, pen_css, ui_jq_css, jq_select_box_css, kashana_scss,
    filters=['cssmin', 'cssrewrite'],
    output='kashana/all.css')

admin_css = Bundle('scss/admin.scss',
                   filters=['pyscss', 'cssmin'],
                   output='kashana/admin.css',
                   depends='scss/**/*.scss')

register('css_all', css_all)
register('css_tables', django_tables_css)
register('css_admin', admin_css)
