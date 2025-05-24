from Mir import LanguageServer
from Mir.runtime import deno
from Mir.api import ActivityIndicator
from Mir.package_storage import PackageStorage, run_command
import sublime


server_storage = PackageStorage(__package__, tag='0.0.1', sync_folder="./language-server")


class BiomeLanguageServer(LanguageServer):
    name='biome'
    activation_events={
        'selector': 'source.js | source.ts | source.jsx | source.tsx | source.js.jsx | source.js.react | source.ts.react | source.css | text.html.basic',
    }
    settings_file="Mir-biome.sublime-settings"

    async def activate(self):
        # setup runtime and install dependencies
        await deno.setup()
        server_path = server_storage / "language-server" / "node_modules" / '@biomejs' / 'biome' / 'bin' / 'biome'
        if not server_path.exists():
            with ActivityIndicator(sublime.active_window(), f'installing {self.name}'):
                await run_command([deno.path, "install"], cwd=str(server_storage / "language-server"))

        # start process
        await self.connect('stdio', {
            'cmd': [deno.path, 'run', '-A', server_path, 'lsp-proxy']
        })
