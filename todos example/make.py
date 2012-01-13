#!/usr/bin/env python

import os, string

ROOT_FILE = 'index.html'
START_JS = '[JS]'
END_JS = '[/JS]'
START_LESS = '[LESS]'
END_LESS = '[/LESS]'
BUILD_PATH = "_site/"
JS_TAG = "<script type='text/javascript' src='js.js'></script>"
CSS_TAG = "<link href='css.css' rel='stylesheet' type='text/css'>"

class ProjectBuilder:
    def __init__(self, filename, mode):
        self.in_js = False
        self.in_less = False
        self.debug = False
        self.release = False
        self.publish = False
        self.clean()
        self.makedir()
        self._index_fh = open("./" + BUILD_PATH + "index.html", 'a')

        if mode == 'd':
            self.debug = True
        elif mode == 'r':
            self.release = True
        elif mode == 'p':
            self.release = True
            self.publish = True

        if not os.path.isfile(filename):
            print "Can't read", filename
            sys.exit(1)

        self.fn = filename

    def copy_file(self, fn):
        import re, shutil, os
        m = re.search('^\.\/(.*)$', fn)
        nfn = m.group(1)
        m = re.search('^(.*)\/.*', nfn)
        nfd = m.group(1)
        try:
            os.makedirs("./_site/" + nfd)
        except os.error:
            pass
        shutil.copy(fn, "./" + BUILD_PATH + nfn)
        

    def concat_less_file(self, fn):
        fn = fn + ".less"
        fd = "./less/" + fn
        nfn = BUILD_PATH + "less.less"
        self.concat(fd, nfn)
    
    def concat(self, fn1, fn2):
        o = open(fn2, "a")
        o.write(open(fn1,'r').read())
        o.close()

    def concat_js_file(self, fn):
        fn = fn + ".js"
        fd = "./js/" + fn
        nfn = BUILD_PATH + "js.big.js"
        self.concat(fd, nfn)

    def include_js_file(self, fn):
        if self.debug:
            self._index_fh.write("<script type='text/javascript' src='js/" + fn + ".js'></script>")
            self.copy_file("./js/" + fn + ".js")

        if self.release:
            self.concat_js_file(fn)

    def include_less_file(self, fn):
        self.concat_less_file(fn)

    def include_line(self, l):
        self._index_fh.write(l)

    def include_css_tag(self):
        self._index_fh.write(CSS_TAG)

    def include_js_tag(self):
        self._index_fh.write(JS_TAG)

    def minify_less(self):
        from subprocess import call
        if self.debug:
            call(["lessc " + BUILD_PATH + "less.less > " + BUILD_PATH + "css.css"], shell=True)
        elif self.release:
            call(["lessc -x " + BUILD_PATH + "less.less > " + BUILD_PATH + "css.css"], shell=True)

    def minify_js(self):
        from subprocess import call
        import os
        call(["uglifyjs " + BUILD_PATH + "js.big.js > " + BUILD_PATH + "js.js"], shell=True)
        os.remove(BUILD_PATH + "js.big.js")


    def copy_images(self):
        import shutil
        shutil.copytree("./img/", BUILD_PATH + "img/")

    def clean(self):
        from shutil import rmtree
        rmtree("./" + BUILD_PATH, True)

    def makedir(self):
        from os import mkdir
        os.mkdir("./" + BUILD_PATH)

    def close_fh(self):
        self._index_fh.close()

    def parse_file(self):
        with open(self.fn) as f:
            for l in f:
                l = l.strip()
                if string.strip(l) == '':
                    continue

                if l == START_JS:
                    self.in_js = True
                    if self.release:
                        self.include_js_tag()
                elif l == END_JS:
                    self.in_js = False
                elif l == START_LESS:
                    self.in_less = True
                    self.include_css_tag()
                elif l == END_LESS:
                    self.in_less = False
                elif self.in_js:
                    if self.debug:
                        self.include_js_file(l)
                    elif self.release:
                        self.concat_js_file(l)
                elif self.in_less:
                    self.include_less_file(l)
                else:
                    self.include_line(l)

        if self.release:
            self.minify_js()

        self.minify_less()
        self.copy_images()

        self.close_fh()

        if self.publish:
            from subprocess import call
            call(["git push . asdfkjakdsfj"], shell=True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Perform various release operations')
    parser.add_argument('operation', type=str,
        help='The operation to perform. [d=debug, r=release, p=publish]', choices=('drp'))

    args = parser.parse_args()

    op = args.operation

    pb = ProjectBuilder(ROOT_FILE, op)
    pb.parse_file()
