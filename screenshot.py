import os
from PIL import ImageGrab # from PIL or PILLOW
from Tkinter import Tk
from tkFileDialog import asksaveasfile
import tkMessageBox
import subprocess
 
 if __name__=='__main__':
      
	      # hide the Tk window
		      root = Tk()
			      root.withdraw()
				       
					       # grab the image from the clipboard
						       myimage = ImageGrab.grabclipboard()
							        
									    # quit if it's not an image
										    if myimage is None:
											        msg = "The clipboard does not contain an image."
													        tkMessageBox.showwarning("Error", msg)
															        exit()
																	     
																		     # choose where to save the file
																			     fout = asksaveasfile(mode='w', defaultextension=".png")
																				      
																					      # quit if the user canceled saving the file
																						      if fout is None:
																							          exit()
																									       
																										       # finally, save the file (extension will dictate the compression)
																											       try:
																												           output = fout.name
																														           myimage.save(output)
																																       except Exception, e:
																																	           msg = "Error: %s" % e
																																			           tkMessageBox.showerror("Error", msg)
																																					       else:
																																						           filePath = os.path.abspath(output)
																																								           #tkMessageBox.showinfo("Saved", filePath)
																																										           subprocess.Popen(r'explorer /select,"'+filePath+'"')
