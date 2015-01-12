import smtplib
import email.utils
from email.MIMEText import MIMEText
from biomaj.workflow import Workflow
import logging

class Notify:
  '''
  Send notifications
  '''

  @staticmethod
  def notifyBankAction(bank):
    if not bank.config.get('mail.smtp.host'):
      logging.info('Notify:none')
      return
    logging.info('Notify:'+bank.config.get('mail.admin'))
    mfrom = bank.config.get('mail.from')
    mto = bank.config.get('mail.admin')
    log_file = bank.config.log_file
    msg = MIMEText('')
    if log_file:
      fp = open(log_file, 'rb')
      msg = MIMEText(fp.read())
      fp.close()
    msg['To'] = email.utils.formataddr(('Recipient', mto))
    msg['From'] = email.utils.formataddr(('Author', mfrom))
    #msg['Subject'] = 'BANK['+bank.name+'] - STATUS['+str(bank.session.get_status(Workflow.FLOW_OVER))+'] - UPDATE['+str(bank.session.get('update'))+'] - REMOVE['+str(bank.session.get('remove'))+']'
    if bank.session.get('action') == 'update':
      msg['Subject'] = 'BANK['+bank.name+'] - STATUS['+str(bank.session.get_status(Workflow.FLOW_OVER))+'] - UPDATE['+str(bank.session.get('update'))+'] - REMOVE['+str(bank.session.get('remove'))+']' + ' - RELEASE['+str(bank.session.get('release'))+']'
    else:
      msg['Subject'] = 'BANK['+bank.name+'] - STATUS['+str(bank.session.get_status(Workflow.FLOW_OVER))+'] - UPDATE['+str(bank.session.get('update'))+'] - REMOVE['+str(bank.session.get('remove'))+']'
    server = None
    try:
      server = smtplib.SMTP(bank.config.get('mail.smtp.host'))
      #server.set_debuglevel(1)
      if bank.config.get('mail.tls') is not None and str(bank.config.get('mail.tls')) == 'true':
        server.starttls()
      if bank.config.get('mail.user') is not None and str(bank.config.get('mail.user')) != '':
        server.login(bank.config.get('mail.user'),bank.config.get('mail.password'))
      server.sendmail(mfrom, [mto], msg.as_string())
    except Exception as e:
      logging.error('Could not send email: '+str(e))
    finally:
      if server is not None:
        server.quit()
