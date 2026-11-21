$env:PATH = "$env:USERPROFILE\AppData\Local\Programs\Git\cmd;$env:USERPROFILE\AppData\Local\Programs\gh;" + $env:PATH
$dir = "$env:USERPROFILE\Downloads\antigravity ai income\03_Active_MVP_09\frontend"
Set-Location $dir

gh repo create Venom1129-dead/cyberdash-game --public --source=. --remote=origin --push
gh api --method POST "repos/Venom1129-dead/cyberdash-game/pages" -f "source[branch]=main" -f "source[path]=/"
