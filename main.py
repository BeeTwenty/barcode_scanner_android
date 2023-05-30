from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import cv2
from pyzbar import pyzbar

class BarcodeScannerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        label_workbook = Label(text="Workbook path:")
        layout.add_widget(label_workbook)

        workbook_entry = TextInput()
        layout.add_widget(workbook_entry)

        browse_button = Button(text="Browse")
        browse_button.bind(on_release=self.browse_workbook)
        layout.add_widget(browse_button)

        scan_button = Button(text="Scan")
        scan_button.bind(on_release=self.scan_barcode)
        layout.add_widget(scan_button)

        return layout
    
    def browse_workbook(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.select_workbook)
        popup = Popup(title='Select Workbook', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def select_workbook(self, instance, path):
        self.workbook_entry.text = path[0]
        instance.parent.parent.dismiss()  # Close the popup

    def scan_barcode(self, instance):
        workbook_path = self.workbook_entry.text

        # Initialize the video capture
        video_capture = cv2.VideoCapture(0)

        while True:
            # Read a frame from the camera
            ret, frame = video_capture.read()

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect barcodes in the frame
            barcodes = pyzbar.decode(gray)

            # Process each barcode detected
            for barcode in barcodes:
                # Extract the barcode data
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                # Perform any necessary operations with the barcode data
                print("Barcode Type:", barcode_type)
                print("Barcode Data:", barcode_data)

                # Close the video capture and exit the loop
                video_capture.release()
                return

            # Display the frame in a window (optional)
            cv2.imshow("Barcode Scanner", frame)

            # Check for key press to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture
        video_capture.release()

        # Close any OpenCV windows
        cv2.destroyAllWindows()

BarcodeScannerApp().run()