mv ui/* .
rm -rf ui/ api/ tooling/ .gitignore LICENSE README.* *.sh
sed -i -e 's/http:\/\/localhost:5000/https:\/\/myntt.pythonanywhere.com/g' index.html
echo "DEPLOYED!!!"
