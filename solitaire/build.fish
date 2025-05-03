#!/usr/bin/fish

if test "$argv[1]" = "clean"
    echo "Cleaning up..."
    rm -fr src/build

    for cachefile in (find . -name "*-pygbag.*")
        rm $cachefile
    end
    set -e argv[1]
end

if test "$argv[1]" = "run"
    pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl --cdn https://pygame-web.github.io/pygbag/0.0/ src
else if test "$argv[1]" = "build"
    pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl --cdn https://pygame-web.github.io/pygbag/0.0/ --build src
end
