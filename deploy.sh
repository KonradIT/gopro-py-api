echo -ne "Version number: "; read version
echo "Releasing version.... $version"
sudo python setup.py sdist
twine upload "dist/goprocam-$version.tar.gz"

if [ ! -z "$GITHUB_TOKEN" ]
then
	echo "GITHUB_TOKEN is empty!"
	exit 1
fi

echo "GitHub release name:"
read name
echo "GitHub release desc:"
read desc

github-release release \
	--security-token $GITHUB_TOKEN \
	--user konradit \
	--repo gopro-py-api \
	--tag "v$version" \
	--name "\"$name\"" \
	--description "\"$desc\"" 

github-release upload \
	--security-token $GITHUB_TOKEN \
	--user konradit \
	--repo gopro-py-api \
	--tag "v$version" \
	--name "goprocam-$version.tar.gz" \
	--file "dist/goprocam-$version.tar.gz"
