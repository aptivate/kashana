var gulp = require('gulp'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    gulpif = require('gulp-if'),
    rjs  = require('gulp-requirejs'),
    qunit  = require('gulp-qunit'),
    handlebars = require('gulp-handlebars'),
    defineModule = require('gulp-define-module'),
    declare = require('gulp-declare'),

    requirejs_config = require('./src/require.config.json'),

    errorCode = 0;

/*****************************
 * HELPERS
 *****************************/
function skipLibDir(file) {
    return file.path.search("lib/") >= 0 ? false : true;
}

/*****************************
 * TASKS
 *****************************/
gulp.task('test', function () {
    gulp.src('./tests/test_runner.html')
        .pipe(qunit())
        .on('error', function(err) {
            errorCode = 1;
            process.emit('exit');
        });;
});

gulp.task('jshint', function (){
    return gulp.src('src/**/*.js')
        .pipe(gulpif(skipLibDir, jshint('.jshintrc')))
        .pipe(jshint.reporter('default'));
});

gulp.task('templates', function () {
    var stream = gulp.src(['src/templates/*.handlebars'])
        .pipe(handlebars())
        .pipe(defineModule('plain'))
        .pipe(declare({
          namespace: 'Aptivate.data.templates'
        }))
        .pipe(concat('src/lib/templates.js'))
        .pipe(gulp.dest('.'));
    return stream;
});

gulp.task('default', ['templates', 'jshint'], function(t){
    requirejs_config.baseUrl = "./src/";
    requirejs_config.out = "logframe.js";
    requirejs_config.name = "main";
    requirejs_config.findNestedDependencies = true;

    return rjs(requirejs_config)
        .pipe(gulp.dest('dist'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
});

/*****************************
 * WATCHERS
 *****************************/
gulp.task('watch', function () {
    gulp.watch('src/templates/**/*.handlebars', ['templates']);
    gulp.watch('src/**/*.js', ['jshint']);
});


/*
 * Report error codes for tests
 */
process.on('exit', function () {
      process.exit(errorCode);
});
