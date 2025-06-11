from Mir import LanguageServer, deno, LoaderInStatusBar, PackageStorage, command


server_storage = PackageStorage(tag='0.0.1')
server_path = server_storage / "language-server" / "node_modules" / '@biomejs' / 'biome' / 'bin' / 'biome'

async def package_storage_setup():
    if server_path.exists():
        return
    await deno.setup()
    server_storage.copy("./language-server")
    with LoaderInStatusBar(f'installing biome'):
        await command([deno.path, "install"], cwd=str(server_storage / "language-server"))

class BiomeLanguageServer(LanguageServer):
    name='biome'
    activation_events={
        'selector': 'source.js | source.ts | source.jsx | source.tsx | source.js.jsx | source.js.react | source.ts.react | source.css | text.html.basic',
    }
    settings_file="Mir-biome.sublime-settings"

    async def activate(self):
        # setup runtime and install dependencies
        await package_storage_setup()

        # start process
        await self.connect('stdio', {
            'cmd': [deno.path, 'run', '-A', server_path, 'lsp-proxy']
        })
