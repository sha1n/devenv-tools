
clean:
	make -C ./inspector-pkg clean
	make -C ./installer-pkg clean
	make -C ./dump-pkg clean

test:
	make -C ./inspector-pkg test
	make -C ./inspector-pkg install
	make -C ./installer-pkg test
	make -C ./dump-pkg test
	make -C ./inspector-pkg uninstall

install:
	make -C ./inspector-pkg install
	make -C ./installer-pkg install
	make -C ./dump-pkg install

uninstall:
	make -C ./inspector-pkg uninstall
	make -C ./installer-pkg uninstall
	make -C ./dump-pkg uninstall

run-support-dump:
	python3 -c 'from dump.tarball import tarball; tarball()' -m=debug

run-installer:
	python3 -c 'from installer.install import install; install()' -m=debug --dryrun
