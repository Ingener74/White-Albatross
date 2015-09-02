/**
 * Created by Pavel on 01.09.2015.
 */

var gulp = require('gulp'),
    clean = require('gulp-clean'),
    connect = require('gulp-connect'),
    run_sequence = require('run-sequence'),
    gh_pages = require('gulp-gh-pages');

// Delete all files in dist
gulp.task('clean', function () {
    return gulp.src('./build/*')
        .pipe(clean());
});

gulp.task('deploy', function () {
    return gulp.src('./build/**/*')
        .pipe(gh_pages({
            force: true
        }));
});

gulp.task('connect', function () {
    connect.server({
        root: './build',
        livereload: true
    });
});

// Copy html
gulp.task('html', function () {
    gulp.src('./app/*.html')
        .pipe(gulp.dest('./build'))
        .pipe(connect.reload());
});

// Copy java script files
gulp.task('js', function () {
    gulp.src('bower_components/bootstrap/dist/js/*.min.js')
        .pipe(gulp.dest('./build/js'))
        .pipe(connect.reload());
});

// Copy css files
gulp.task('css', function () {
    gulp.src('bower_components/bootstrap/dist/css/*.min.css')
        .pipe(gulp.dest('./build/css'))
        .pipe(connect.reload());
});

gulp.task('build', function (callback) {
    run_sequence('clean', ['html', 'js', 'css'], callback);
});

gulp.task('watch', function () {
    gulp.watch(['./app/*.html'], ['build'])
});

gulp.task('default', ['connect', 'build', 'watch']);

