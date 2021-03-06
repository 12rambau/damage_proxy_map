from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v

from component import widget as cw
from component.scripts import * 

class DmpTile(sw.Tile):
    
    def __init__(self, aoi_io, dmp_io):
        
        # gather the io as class attribute 
        self.aoi_io = aoi_io 
        self.io = dmp_io
        
        # create the widgets 
        self.date_picker = sw.DatePicker(label = 'Disaster event date')
        self.username = v.TextField(
            label = "Copernicus Scihub Username",
            v_model = None
        )
        self.password = cw.PasswordField(label = "Copernicus Scihub Password")
        
        
        # bind them with the output 
        self.output = sw.Alert() \
            .bind(self.date_picker, self.io, 'event') \
            .bind(self.username, self.io, 'username') \
            .bind(self.password.text_field, self.io, 'password')
        
        self.btn = sw.Btn("Launch the process")
        
        # construct the tile 
        super().__init__(
            id_ = "process_widget",
            title = "Damage proxy map",
            inputs = [self.date_picker, self.username, self.password],
            output = self.output,
            btn = self.btn
        )
        
        # link the click to an event 
        self.btn.on_event('click', self._on_click)
        
    def _on_click(self, widget, data, event):
        
        widget.toggle_loading()
        
        if not self.output.check_input(self.aoi_io.get_aoi_name(), 'no aoi'): return widget.toggle_loading()
        if not self.output.check_input(self.io.username, 'no username'): return widget.toggle_loading()
        if not self.output.check_input(self.io.password, 'no password'): return widget.toggle_loading()
        
        try:
            check_computer_size(self.output)
            create_dmp(self.aoi_io, self.io, self.output)
        
            self.output.add_live_msg('Computation complete', 'success')
        
        except Exception as e: 
            self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        
        return
        