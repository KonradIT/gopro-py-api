version=$(jq -r .release_version version.json)
echo "Releasing version.... $version"
echo -ne "Change version? [Y/n]: "; read choice
if [ "$choice" == "Y" ]; then
	echo -ne "Version number: "; read new_version
	tmp=$(mktemp)
	jq ".release_version = \"$new_version\"" version.json > "$tmp" && mv "$tmp" version.json
fi

version=$(jq -r .release_version version.json)
echo "Releasing version.... $version"
python setup.py sdist
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
    --name "$name" \
    --description "$desc" 

github-release upload \
	--security-token $GITHUB_TOKEN \
	--user konradit \
    --repo gopro-py-api \
    --tag "v$version" \
	--name "goprocam-$version.tar.gz"
	--file "dist/goprocam-$version.tar.gz"