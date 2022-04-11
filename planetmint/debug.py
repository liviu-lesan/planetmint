import ptvsd
print("#####\nAttaching\n")
ptvsd.enable_attach(("0.0.0.0", 2222))  #, redirect_output=True)
print("#####\nWait for Attaching\n")
print("#####\nWait for Attaching\n")
ptvsd.wait_for_attach()  # from gevent import monkey; monkey.patch_all()
