import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, server, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def execute_notebook(nb_in, nb_out):
    with open(nb_in) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=1200, kernel_name='Python 3')

    try:
        out = ep.preprocess(nb)
    except CellExecutionError:
        out = None
        msg = 'Error executing the notebook "{}".\n\n'.format(nb_in)
        msg += 'See notebook "{}" for the traceback.'.format(nb_out)
        print(msg)
        raise
    finally:
        with open(nb_out, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)


if __name__ == '__main__':
    execute_notebook(nb_in='data_validation_base.ipynb', nb_out='data_validation_executed.ipynb')

    send_mail(send_from='ABC@ABC.com',
              send_to=['DEF@DEF.com'],
              subject='Test',
              text='Hello!',
              server='server.com',
              files=['data_validation.html'])
