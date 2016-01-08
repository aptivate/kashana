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
	    uglify: {
	    	logframe: {
	    		'dist/logframe.min.js': ['src/**/*.js']
	    	}
	    },
	    watch: {
	      files: ['src/**/*.js'],
	      tasks: ['gulp:templates', 'jshint']
	    },
	    // Based on https://github.com/maenu/grunt-template-jasmine-istanbul-example/blob/requirejs-client/Gruntfile.js at 30/11/2015
		jasmine: {
			coverage: {
				src: ['src/**/*.js', "!src/lib/*.js", "!src/lib/**/*.js"],
				options: {
					keepRunner: true,
					vendor:[
					        'tests/lib/fixtures.js',
					        'node_modules/jquery/dist/jquery.js',
			        ],
					specs: [
					        'tests/js/list-tests.js', 
					        'tests/js/input-tests.js',
					        'tests/js/item-show-hide-tests.js',
					        'tests/js/filter-lead-tests.js',
					        'tests/js/filter-date-tests.js',
					        'tests/js/editables/feedback-mixin-tests.js',
					        'tests/js/editables/cleaninput-mixin-tests.js',
					        'tests/js/components/base-view-tests.js',
					],
					helpers: [
					          'node_modules/jasmine2-custom-message/jasmine2-custom-message.js',
					          'node_modules/jasmine-jquery/lib/jasmine-jquery.js'
		            ],
					template: require('grunt-template-jasmine-istanbul'),
					templateOptions: {
						coverage: '../reports/coverage.json',
						report: [
							{
								type: 'cobertura',
								options: {
									dir: '../reports/'
								}
							},
						],
						// 1. don't replace src for the mixed-in template with instrumented sources
						replace: false,
						template: require('grunt-template-jasmine-requirejs'),
						templateOptions: {
							requireConfigFile: 'src/require.config.js',
							requireConfig: {
								// 2. use the baseUrl you want
								
								baseUrl: 'src/',
								// 3. pass paths of the sources being instrumented as a configuration option
								//    these paths should be the same as the jasmine task's src
								//    unfortunately, grunt.config.get() doesn't work because the config is just being evaluated
								config: {
									instrumented: {
										src: grunt.file.expand('src/**/*.js', "!src/lib/*.js")
									}
								},
								// 4. use this callback to read the paths of the sources being instrumented and redirect requests to them appropriately
								callback: function () {
									define('instrumented', ['module'], function (module) {
										return module.config().src;
									});
									require(['instrumented'], function (instrumented) {
										var oldLoad = requirejs.load;
										requirejs.load = function (context, moduleName, url) {
											// normalize paths
											if (url.substring(0, 1) == '/') {
												url = url.substring(1);
											} else if (url.substring(0, 2) == './') {
												url = url.substring(2);
											}
											// redirect
											if (instrumented.indexOf(url) > -1) {
												url = './.grunt/grunt-contrib-jasmine/' + url;
											}
											return oldLoad.apply(this, [context, moduleName, url]);
										};
									});
								}
							}
						}
					}
				}
			}
		}
	  });

	  grunt.loadNpmTasks('grunt-contrib-uglify');
	  grunt.loadNpmTasks('grunt-contrib-jshint');
	  grunt.loadNpmTasks('grunt-contrib-jasmine');
	  grunt.loadNpmTasks('grunt-contrib-watch');
	  
	  grunt.loadNpmTasks('grunt-gulp');

	  grunt.registerTask('test', ['jasmine']);
	  
	  grunt.registerTask('templates', ['gulp:templates']);

	  grunt.registerTask('default', ['templates', 'jshint']);

};
