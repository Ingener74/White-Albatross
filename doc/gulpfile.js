/**
 * Created by Pavel on 01.09.2015.
 */

var gulp = require('gulp'),
    clean = require('gulp-clean'),
    connect = require('gulp-connect'),
    runSequence = require('run-sequence'),
    ghPages = require('gulp-gh-pages');

var paths = {
    app: 'app',
    dist: 'build',
    dist_js: 'build/js',
    dist_css: 'build/css',
    bootstrap: 'bower_components/bootstrap/dist'
};

var files = {
    main: paths.app + '/index.html',
    images: paths.app + '/*png',
    js_files: '/js/*.min.js',
    css_files: '/css/*.min.css'
};

// Delete all files in dist
gulp.task('clean', function () {
    return gulp.src(paths.dist + '/*')
        .pipe(clean());
});

gulp.task('deploy', function () {
    return gulp.src(paths.dist + '/**/*')
        .pipe(ghPages());
});

gulp.task('connect', function () {
    connect.server({
        root: paths.dist,
        livereload: true
    });
});

// Copy html
gulp.task('html', function () {
    gulp.src(paths.app + '/*.html')
        .pipe(gulp.dest(paths.dist))
        .pipe(connect.reload());
});

// Copy java script files
gulp.task('js', function () {
    gulp.src(paths.bootstrap + files.js_files)
        .pipe(gulp.dest(paths.dist + '/js'))
        .pipe(connect.reload());
});

// Copy css files
gulp.task('css', function () {
    gulp.src(paths.bootstrap + files.css_files)
        .pipe(gulp.dest(paths.dist + '/css'))
        .pipe(connect.reload());
});

gulp.task('build', function (callback) {
    runSequence('clean', ['html', 'js', 'css'], callback);
});

gulp.task('watch', function () {
    gulp.watch([paths.app + '/*.html'], ['build'])
});

gulp.task('default', ['connect', 'build', 'watch']);

