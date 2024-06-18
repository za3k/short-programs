INSTALL=/usr/bin
open-directory-install:
	sudo cp open-directory ${INSTALL}/open-directory
	sudo cp open-directory.desktop /usr/local/share/applications/open-directory.desktop 
	xdg-mime default open-directory.desktop inode/directory
	xdg-mime default open-directory.desktop application/x-directory
	sudo xdg-mime default open-directory.desktop inode/directory
	sudo xdg-mime default open-directory.desktop application/x-directory
	sudo update-desktop-database
open-text-file-install:
	sudo cp open-text-file ${INSTALL}/open-text-file
	sudo cp open-text-file.desktop /usr/local/share/applications/open-text-file.desktop 
	xdg-mime default open-text-file.desktop text/plain
	sudo xdg-mime default open-text-file.desktop text/plain
	update-desktop-database
install:
	find -executable -type f | sudo xargs cp -t ${INSTALL}
