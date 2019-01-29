import os
import sys
import sublime
import sublime_plugin

if sys.version_info >= (3,):
    import importlib
    import zipimport

st_build = int(sublime.version())
mod_prefix = 'sync_settings'
bare_mod_prefix = mod_prefix

# ST3 loads each package as a module, so it needs an extra prefix
if sys.version_info >= (3,):
    mod_prefix = 'SyncSettings.' + mod_prefix
    from imp import reload

# When reloading the package, we also need to reload the base "sync_settings"
# module in ST3. This flag inidicates we should re-add the PC package path
# to the beginning of sys.path before we try to reload.
do_insert = False
is_zipped = False

commands_name = mod_prefix + '.commands'
pc_package_path = os.path.dirname(__file__)
if commands_name in sys.modules and sys.version_info >= (3,) and st_build < 3112:
    # Unfortunately with ST3, the ZipLoader does not "properly"
    # implement load_module(), instead loading the code from the zip
    # file when the object is instantiated. This means that calling
    # reload() by itself does nothing. Instead we have to refresh the
    # actual source code and then call reload().
    if pc_package_path.endswith('.sublime-package'):
        refreshing_zip_loader = sublime_plugin.ZipLoader(pc_package_path)
        pc_zip_loader = sys.modules[commands_name].__loader__
        if hasattr(pc_zip_loader, 'contents') and hasattr(pc_zip_loader, 'packages'):
            pc_zip_loader.contents = refreshing_zip_loader.contents
            pc_zip_loader.packages = refreshing_zip_loader.packages

        if pc_package_path in zipimport._zip_directory_cache:
            del zipimport._zip_directory_cache[pc_package_path]
        is_zipped = True

    importlib.invalidate_caches()
    do_insert = True

# Python allows reloading modules on the fly, which allows us to do live upgrades.
# The only caveat to this is that you have to reload in the dependency order.
#
# Thus is module A depends on B and we don't reload B before A, when A is reloaded
# it will still have a reference to the old B. Thus we hard-code the dependency
# order of the various SyncSettings modules so they get reloaded properly.
#
# There are solutions for doing this all programatically, but this is much easier
# to understand.
reload_mods = []
for mod in sys.modules:
    if mod.startswith(('sync_settings', 'SyncSettings')) and sys.modules[mod] is not None:
        reload_mods.append(mod)

mods_load_order = [
    '',

    '.libs',
    '.libs.logger',
    '.libs.path',
    '.libs.settings',
    '.libs.gist',

    '.thread_progress',
    '.sync_version',
    '.sync_manager',

    '.commands',
    '.commands.decorators',
    '.commands.open_logs',
    '.commands.download',
    '.commands.upload',
    '.commands.create_and_upload',
    '.commands.delete_and_create',
]

loaders = dict()
if do_insert:
    if is_zipped:
        # When we run into modules imports from a .sublime-package, the
        # in memory modules reference a zipimport.zipimporter object that
        # has an out-dated reference to the .sublime-package file, which
        # means when we call reload(), we get a zipimport.ZipImportError
        # of "bad local file header". To work around this, we construct
        # new zipimporter instances and attach them to the in-memory
        # modules using the .__loader__ attribute.
        loaders[''] = zipimport.zipimporter(pc_package_path)
    else:
        sys.path.insert(0, pc_package_path)

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except (ImportError):
            pass  # Upgrade issues from PC 2.0 -> 3.0

    if sys.version_info >= (3,) and st_build < 3112:
        bare_mod = bare_mod_prefix + suffix
        if bare_mod in reload_mods:
            bare_module = sys.modules[bare_mod]
            if is_zipped:
                # See the command above near "if is_zipped:" to understand why
                # we are replacing the .__loader__ attribute of the modules with
                # a fresh zipimporter object.
                if bare_mod.find('.') == -1:
                    loader_lookup = ''
                else:
                    loader_lookup = os.sep.join(bare_mod.split('.')[0:-1])
                    if loader_lookup not in loaders:
                        zi_path = os.path.join(pc_package_path, loader_lookup) + os.sep
                        loaders[loader_lookup] = zipimport.zipimporter(zi_path)
                bare_module.__loader__ = loaders[loader_lookup]
            reload(bare_module)

if do_insert and not is_zipped:
    sys.path.remove(pc_package_path)
