from pathlib import Path
import importlib.util


def discover_plugins():
    """Discover and import all plugins under the plugins directory."""
    plugins = {}
    plugins_dir = Path(__file__).parent / "plugins"
    for path in plugins_dir.glob('**/*.py'):
        if path.name.startswith('_'):
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'Plugin'):
                plugins[path.stem] = module
    return plugins
