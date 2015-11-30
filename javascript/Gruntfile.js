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
	      all: {
			  options: {
				urls: ["http://localhost:8500/tests/test.html"],
				coverage: {
					src: ['src/**/*.js', 'tests/js/*.js'],
					instrumentedFiles: 'temp/',
					coberturaReport: '../reports/',
					htmlReport: 'report/coverage',
					linesThresholdPct: 20
				}
			  }
		  }
	    },
	    qunit_junit: {
		    options: {
		    	dest: '../reports/'
		    }
	    },
	    connect: {
	        server: {
	          options: {
	            port: 8500,
	            base: '.'
	          }
	        }
	    },
	    intern: {
	        grunt: {
	          options: {
	            runType: 'runner', // defaults to 'client'
	            config: 'tests/intern',
	            reporters: [ 'Cobertura' ],
	            suites: [ 'tests/js/test' ],
	            loaders: {
	            	'host-node': 'requirejs',
	               	'host-browser': 'node_modules/requirejs/require.js'
	            }
	          }
	        },
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
	    },
	    jasmine : {
	        src : ['src/**/*.js', "!src/lib/*.js"],
	        options : {
	        	vendor:[
        	        'tests/lib/fixtures.js',
        	        'node_modules/jquery/dist/jquery.js',
	        	],
	            specs : [
	                'tests/js/list-tests.js', 
                    'tests/js/input-tests.js',
                    'tests/js/filter-lead-tests.js',
                    'tests/js/filter-date-tests.js',
                    'tests/js/editables/feedback-mixin-tests.js',
                    'tests/js/editables/cleaninput-mixin-tests.js',
                    'tests/js/components/base-view-tests.js'
	            ],	
	            helpers: [
	                'node_modules/jasmine2-custom-message/jasmine2-custom-message.js',
	                'node_modules/jasmine-jquery/lib/jasmine-jquery.js'
	            ],
	            template: require('grunt-template-jasmine-requirejs'),
	            templateOptions: {
	            	requireConfigFile: 'src/require.config.js',
	 	            requireConfig: {'baseUrl': './src'},
	            },
	    		
	        }
	    }
	  });

	  grunt.loadNpmTasks('grunt-contrib-uglify');
	  grunt.loadNpmTasks('grunt-contrib-jshint');
	  grunt.loadNpmTasks('grunt-contrib-qunit');
	  grunt.loadNpmTasks('grunt-qunit-cov');
	  grunt.loadNpmTasks('grunt-qunit-istanbul');
	  grunt.loadNpmTasks('grunt-contrib-jasmine');
	  grunt.loadNpmTasks('grunt-contrib-watch');
	  grunt.loadNpmTasks('grunt-contrib-concat');
	  grunt.loadNpmTasks('grunt-contrib-connect');
	  grunt.loadNpmTasks('grunt-qunit-junit');
	  grunt.loadNpmTasks('grunt-gulp');

	  grunt.registerTask('test', ['jasmine']);
	  
	  grunt.registerTask('templates', ['gulp:templates']);

	  grunt.registerTask('default', ['templates', 'jshint', 'requirejs']);

};
