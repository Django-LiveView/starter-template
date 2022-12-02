//===
// IMPORTS
//===
const {src, dest, parallel, series, watch} = require('gulp');
const browserSync = require('browser-sync').create();
const clean = require('gulp-clean');
const sass = require('gulp-dart-sass');
const sourcemaps = require('gulp-sourcemaps');
const gaze = require('gaze');

//===
// VARIABLES
//===
const runTimestamp = Math.round(Date.now() / 1000);
const SRC_PATH = 'assets';
const DEST_PATH = 'static';

//===
// TASKS
//===
function cleanDist() {
  return src(
    ['static/img', 'static/css', 'static/fonts', 'static/js'],
    { allowEmpty: true }
  ).pipe(clean());
};

// Static server with reload
function initBrowserSync(cb) {
  browserSync.init({
    notify: false,
    open: false,
    proxy: 'django:8000'
  });
  return cb;
};

// Compile SASS + sourcemaps
function sassCompile() {
  return src([SRC_PATH + "/sass/desktop.sass", SRC_PATH + "/sass/mobile.sass"])
    .pipe(sourcemaps.init())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(sourcemaps.write('.'))
    .pipe(dest(DEST_PATH + '/css/'))
    .pipe(browserSync.stream());
};

// Copy images
function images() {
  return src(SRC_PATH + '/img/**/*')
    .pipe(dest(DEST_PATH + '/img/'))
    .pipe(browserSync.stream());
};

// Copy fonts
function fonts() {
  return src(SRC_PATH + "/fonts/**/*")
    .pipe(dest(DEST_PATH + "/fonts/"))
    .pipe(browserSync.stream());
}

// Compile JavaScript
function javascript() {
  return src([SRC_PATH + '/js/*.js', SRC_PATH + '/js/**/*.js'])
    .pipe(dest(DEST_PATH + '/js/'))
    .pipe(browserSync.stream());
}

//===
// Tasks
//===

// Default: 'gulp'
const build = series(
  cleanDist,
  parallel(sassCompile, images, fonts, javascript)
);
exports.default = build;

// Dev: 'gulp dev'
exports.dev = function () {
  build();

  gaze([SRC_PATH + '/sass/*.sass', SRC_PATH + '/sass/**/*.sass'], function(err, watcher) {
    this.on('all', sassCompile);
  });
  gaze([SRC_PATH + '/img/*', SRC_PATH + '/img/**/*'], function(err, watcher) {
    this.on('all', images);
  });

  gaze([SRC_PATH + '/fonts/*', SRC_PATH + '/fonts/**/*'], function(err, watcher) {
    this.on('all', fonts);
  });

  gaze([SRC_PATH + '/js/*.js', SRC_PATH + '/js/**/*.js'], function(err, watcher) {
    this.on('all', javascript);
  });

  initBrowserSync();
}
