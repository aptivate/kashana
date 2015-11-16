var gulp = require('gulp'),
    handlebars = require('gulp-handlebars'),
    defineModule = require('gulp-define-module'),
    declare = require('gulp-declare'),
    concat = require('gulp-concat');

module.exports = function(grunt) {
	grunt.initConfig({
	    pkg: grunt.file.readJSON('package.json'),
	    jshint: {
	    	'logframe': ['src/**/*.js'],
	    	'ignores': ['src/**/lib/**/lib/**/*.js']
	    },
	    qunit: {
	      src: ['./tests/test_runner.html'],
		  options: {
			coverage: {
				src: ['src/**/*.js'],
				instrumentedFiles: 'temp/',
				coberturaReport: '../reports/',
				htmlReport: 'report/coverage',
				linesThresholdPct: 20
			}
		  }
	    },
	    qunit_junit: {
		    options: {
		    	dest: '../reports/'
		    }
	    },
	    watch: {
	      files: ['src/**/*.js'],
	      tasks: ['jshint', 'qunit']
	    },
	    gulp: {
	    	templates: function (){
	    		return gulp.src(['src/templates/*.handlebars'])
	            .pipe(handlebars())
	            .pipe(defineModule('plain'))
	            .pipe(declare({
	              namespace: 'Aptivate.data.templates'
	            }))
	            .pipe(concat('src/lib/templates.js'))
	            .pipe(gulp.dest('.'));
	    	}
	    }
	  });

	  grunt.loadNpmTasks('grunt-contrib-uglify');
	  grunt.loadNpmTasks('grunt-contrib-jshint');
	  grunt.loadNpmTasks('grunt-contrib-qunit');
	  grunt.loadNpmTasks('grunt-qunit-cov');
	  grunt.loadNpmTasks('grunt-qunit-istanbul');
	  grunt.loadNpmTasks('grunt-contrib-watch');
	  grunt.loadNpmTasks('grunt-contrib-concat');
	  grunt.loadNpmTasks('grunt-qunit-junit');
	  grunt.loadNpmTasks('grunt-gulp');

	  grunt.registerTask('test', ['qunit', 'qunit_junit']);

	  grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);

};
