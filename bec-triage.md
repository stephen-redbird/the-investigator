##BEC fraud email example
#BEC Triage – Meridian Group wire-transfer email

#Email:
FROM:    Marcus Webb <marcus.webb@meridiangroup.com>
TO:      Sandra Kowalski <s.kowalski@meridiangroup.com>
SUBJECT: URGENT — Wire Transfer Needed Today
DATE:    Friday, March 20, 2026, 4:31 PM

Sandra,
I need you to process a wire transfer immediately. I am in meetings
in Singapore and cannot be reached by phone until Monday.

Amount:    $84,000.00 USD
Recipient: Apex Consulting Group
Bank:      First National Bank of Nevada
Account:   7742-9901-3348

This is time-sensitive. The vendor has a hard deadline of 5 PM today.
Please confirm once sent. Do not discuss this with anyone else on the
team — it relates to a confidential acquisition and premature
disclosure could affect the deal.

Marcus
Marcus Webb | CEO, Meridian Group

#Email header metadata:
Received: from mail-lj1-f201.google.com (209.85.208.201)
    by mx.meridiangroup.com; Fri, 20 Mar 2026 16:31:02 -0500
Received: from [192.168.43.7] (unknown [41.223.57.188])
    by smtp.gmail.com; Fri, 20 Mar 2026 14:30:59 -0700
From:       Marcus Webb <marcus.webb@meridiangroup.com>
Reply-To:   mwebb.ceo2026@gmail.com
X-Originating-IP: 41.223.57.188
Authentication-Results: mx.meridiangroup.com;
    dkim=fail (signature did not verify)
    spf=softfail (domain of transitioning sender)
    dmarc=fail (p=none) header.from=meridiangroup.com

##Verdict
Spoofed (impersonation). Confidence: high.
Reasoning:
-If Marcus Webb's actual corporate account were compromised, the mail would originate from Meridian's real mail servers or from an IP that at least passes SPF/DKIM for meridiangroup.com. It doesn't — it comes from a Gmail account.
-All three authentication mechanisms fail or are weak, consistent with a forged From header rather than a compromised legitimate mailbox.
-The Reply-To redirect to a lookalike personal Gmail address is a classic spoofing/social-engineering artifact, not something that happens with a genuinely compromised account (a compromised account's replies go back to the real account).
-Originating IP geolocates to Africa via a mobile/NAT connection — inconsistent with a CEO's normal corporate or home network, and typical of attacker infrastructure used in these campaigns.

##Red flags found
- Reply-To is a Gmail address, not the company domain
- SPF softfail, DKIM fail, DMARC fail — sender not authorized
- Originating IP (41.223.x.x) is an African ISP, not Singapore
- Urgency (5 PM deadline), secrecy ("don't tell the team"),
  authority (the CEO)
-Sending domain doesn't match the claimed identity.
-Private/NAT address in the header chain.
-has an address that looks similar but isn’t identical

## Verification checklist (before wiring money)
1. Call the CEO back on a known, trusted number (not from the email)
2. Require a second approver for any new payee or wire
3. Check the actual sending domain, not just the display name. 
4. Treat urgency as a red flag, not a reason to skip steps. "Send this in the next hour" or "don't tell anyone else" should trigger more scrutiny, not less. 
5. Independently confirm any change to payee, bank, or account details. If wiring instructions changed from a prior transaction, verify the change directly with the vendor/executive through a known channel first.
6. Flag Reply-To mismatches. If the reply address differs from the sender address, that's an automatic hold-and-verify trigger. 
7. When in doubt, hold the payment and escalate. A short delay to confirm costs nothing; a fraudulent wire sent is almost never recoverable.

