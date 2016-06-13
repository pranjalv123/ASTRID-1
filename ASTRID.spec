# -*- mode: python -*-

block_cipher = None


a = Analysis(['build/bin/ASTRID'],
             pathex=['build/bin/', 'build/bin/lib/python'],
             binaries=[],
             datas=[('build/bin/makemat', '.'), ('build/bin/fastme', '.'), ('build/bin/PhyDstar.jar', '.')],
             hiddenimports=['ASTRID.ASTRID'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ASTRID',
          debug=False,
          strip=False,
          upx=True,
          console=True )
