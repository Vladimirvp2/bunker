from distutils.core import setup
import py2exe
 
setup(
      windows=['App.py'],
      options={"py2exe": {"includes":["aglyph", 'Common.Localization', 'Common.ResourceManager', 'Common.Notifier', 'Common.Utilities',
                                      'Common.Crypt', 'Common.Constants.Colors', 'Common.Constants.DatabaseMerge',
                                      'Common.Constants.DataField', 'Common.Constants.DBObjectType', 
                                      'Common.Constants.DBStatus', 'Common.Constants.Default', 
                                      'Common.Constants.EntryStatus', 'Common.Constants.PasswordStrength',
                                      'Common.Constants.Singal', 'Common.Constants.Table', 
                                      'Common.Constants.LabelType',
                                      
                                       
                                       'GUI.AppMainWin',
                                       'GUI.Dialogs.Login',
                                       
                                       'Controllers.MainWinController',
                                       'Controllers.LoginController',
                                       
                                       'DataModel.DataBaseManager',
                                       'DataModel.UserConfigManager',
                                       
                                       'GUI.MessageDialog'
                                       
                                       ]}},
      #options={"py2exe": {"includes":["sip","qad","dialog","sys","PyQt4"]}},
      data_files=[("Resources",["Resources/resourceConfig.xml"]), 
                  ("Resources/Localization",["Resources/Localization/l_EN.xml"]), 'app_context.xml']
      #             ["bm/large.gif", "bm/small.gif"]),
      #            ("fonts",
       #            )]
      )