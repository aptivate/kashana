var gulp = require('gulp'),
    handlebars = require('gulp-handlebars'),
    defineModule = require('gulp-define-module'),
    declare = require('gulp-declare'),
    concat = require('gulp-concat');

module.exports = function(grunt) {
	grunt.initConfig({
	    pkg: grunt.file.readJSON('package.json'),
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
	    },
	    jshint: {
	    	'logframe': ['src/**/*.js', '!src/lib/*'],
	    	'options': {
	    		'jshintrc': '.jshintrc',
	    	}
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
	    requirejs: {
	    	compile: {
		    	options: {
		    		baseUrl: './src/',
		    		findNestedDependencies: true,
		    		mainConfigFile: './src/require.config.js',
		    		name: 'main',
		    		out: 'dist/logframe.min.js'
		    	}
	    	},
		    copy: {
		    	options: {
		    		baseUrl: './src/',
		    		findNestedDependencies: true,
		    		mainConfigFile: './src/require.config.js',
		    		name: 'main',
		    		out: 'dist/logframe.js',
		    		optimize: 'none'
		    	}
		    }
	    },
	    uglify: {
	    	logframe: {
	    		'dist/logframe.min.js': ['src/**/*.js']
	    	}
	    },
	    watch: {
	      files: ['src/**/*.js'],
	      tasks: ['gulp:templates', 'jshint']
	    }
	  });

	  grunt.loadNpmTasks('grunt-contrib-uglify');
	  grunt.loadNpmTasks('grunt-contrib-jshint');
	  grunt.loadNpmTasks('grunt-contrib-qunit');
	  grunt.loadNpmTasks('grunt-qunit-cov');
	  grunt.loadNpmTasks('grunt-qunit-istanbul');
	  grunt.loadNpmTasks('grunt-contrib-watch');
	  grunt.loadNpmTasks('grunt-contrib-concat');
	  grunt.loadNpmTasks('grunt-requirejs');
	  grunt.loadNpmTasks('grunt-qunit-junit');
	  grunt.loadNpmTasks('grunt-gulp');

	  grunt.registerTask('test', ['qunit', 'qunit_junit']);
	  
	  grunt.registerTask('templates', ['gulp:templates']);

	  grunt.registerTask('default', ['templates', 'jshint', 'requirejs']);

};
