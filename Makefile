INSTALL=/usr/bin
install:
	find -executable -type f | sudo xargs cp -t ${INSTALL}
