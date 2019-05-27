
clean:
	make -C ./inspector-pkg clean
	make -C ./dump-pkg clean

test:
	make -C ./inspector-pkg test
	make -C ./inspector-pkg install
	make -C ./dump-pkg test
	make -C ./inspector-pkg uninstall

install:
	make -C ./inspector-pkg install
	make -C ./dump-pkg install

uninstall:
	make -C ./inspector-pkg uninstall
	make -C ./dump-pkg uninstall

support-dump:
	python3 -c 'from dump.tarball import tarball; tarball()'
