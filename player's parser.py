import json
import csv
import requests

def scrapeing_cat():
    try:
        url = requests.get('http://site.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byathlete?contentorigin=espn&isqualified=true&lang=en&region=us&sort=offensive.avgPoints%3Adesc&limit=400')
    except:
        with open('byathlete.json') as json_file:
            data = json.load(json_file)
    names = []
    # get player's names in to a list and on to the csv file.
    for athlete in data['athletes']:
        names.append(athlete['athlete']['displayName'])

        with open('Name.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            # header in csv
            mywriter.writerow(['Name'])
            # writing the ast stats to row
            for namess in names:
                mywriter.writerow([namess])

    # AST and TO
    sass = []
    for assists in data['athletes']:
        a = list(assists['categories'][1]['totals'][10:12])
        ast = (a[0])
        nast = []
        nast.append(ast)
        fast = list(nast)
        sass = sass + list(map(float, fast))
        new_ast = [[i] for i in sass]

        with open('APG.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            # header in csv
            mywriter.writerow(['APG'])
            # writing the ast stats to row
            for ssa in new_ast:
                mywriter.writerow(ssa)
    # tornovers per game
    fto = []
    for tornovers in data['athletes']:
        t = list(tornovers['categories'][1]['totals'][10:12])[1]
        sto = []
        sto.append(t)
        sto = list(sto)
        fto = fto + list(map(float, sto))
        new_to = [[t] for t in fto]

        with open('TO.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['To'])
            for ot in new_to:
                mywriter.writerow(ot)
    #   0   1   2   3   4   5   6   7   8   9
    # PTS, FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%

    ppg = []
    for points in data['athletes']:
        p = list(points['categories'][1]['totals'][0:9])
        pts = (p[0])
        spts = []
        spts.append(pts)
        fpts = list(spts)
        ppg = ppg + list(map(float, fpts))
        new_pts = [[q] for q in ppg]

    with open('PPG.csv', 'w') as outfile:
        mywriter = csv.writer(outfile)
        mywriter.writerow(['PPG'])
        for stp in new_pts:
            mywriter.writerow(stp)

    # field goals made per game.
    fgm = []
    for field_goals in data['athletes']:
        f = list(field_goals['categories'][1]['totals'][0:9])
        fg = (f[1])
        sfgm = []
        sfgm.append(fg)
        ffgm = list(sfgm)
        fgm = fgm + list(map(float, ffgm))
        new_fgm = [[y] for y in fgm]

        with open('FGM.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['FGM'])
            for mgf in new_fgm:
                mywriter.writerow(mgf)

    # field goals attempted per game.
    fga = []
    for fg_attempt in data['athletes']:
        attem = list(fg_attempt['categories'][1]['totals'][0:9])
        fa = (attem[2])
        sfga = []
        sfga.append(fa)
        ffga = list(sfga)
        fga = fga + list(map(float, ffga))
        new_fga = [[m] for m in fga]

        with open('FGA.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['FGA'])
            for agf in new_fga:
                mywriter.writerow(agf)

    # field goal percentage.
    ggg = []
    for fg_perc in data['athletes']:
        fp = list(fg_perc['categories'][1]['totals'][0:9])
        fgp = (fp[3])
        sfgp = []
        sfgp.append(fgp)
        ffgp = list(sfgp)
        ggg = ggg + list(map(float, ffgp))
        new_fgp = [[l] for l in ggg]

        with open('FG%.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['FG%'])
            for agf in new_fgp:
                mywriter.writerow(agf)

    # 3 pointers made.
    threes_made = []
    for field_goals in data['athletes']:
        three = list(field_goals['categories'][1]['totals'][0:9])
        tpm = (three[4])
        stpm = []
        stpm.append(tpm)
        ftpm = list(stpm)
        threes_made = threes_made + list(map(float, ftpm))
        new_tpg = [[k] for k in threes_made]

        with open('3PM.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['3PM'])
            for pm in new_tpg:
                mywriter.writerow(pm)
    # free throws percent.
    ft = []
    for free_throws in data['athletes']:
        frees = list(free_throws['categories'][1]['totals'][0:10])
        ftp = (frees[-1])
        sftp = []
        sftp.append(ftp)
        ftpg = list(sftp)
        ft = ft + list(map(float, ftpg))
        new_ft = [[u] for u in ft]

        with open('FT%.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['FT%'])
            for tf in new_ft:
                mywriter.writerow(tf)

    # reb per game
    reb = []
    for rebounds in data['athletes']:
        r = list(rebounds['categories'][0]['totals'][-1:])
        rbg = (r[0])
        srbg = []
        srbg.append(rbg)
        frbg = list(srbg)
        reb = reb + list(map(float, frbg))
        new_rbg = [[u] for u in reb]

    with open('RPG.csv', 'w') as outfile:
        mywriter = csv.writer(outfile)
        mywriter.writerow(['RPG'])
        for ber in new_rbg:
            mywriter.writerow(ber)

    # steals per game
    spg = []
    for steals in data['athletes']:
        s = list(steals['categories'][2]['totals'])
        stl = (s[0])
        sstl = []
        sstl.append(stl)
        fstl = list(sstl)
        spg = spg + list(map(float, fstl))
        new_stl = [[k] for k in spg]

    with open('STL.csv', 'w') as outfile:
        mywriter = csv.writer(outfile)
        mywriter.writerow(['STL'])
        for lts in new_stl:
            mywriter.writerow(lts)
    # Blocks for game.
    bpg = []
    for blocks in data['athletes']:
        b = list(blocks['categories'][2]['totals'])
        blk = (b[1])
        sblk = []
        sblk.append(blk)
        fblk = list(sblk)
        bpg = bpg + list(map(float, fblk))
        new_blk = [[x] for x in bpg]

        with open('BLK.csv', 'w') as outfile:
            mywriter = csv.writer(outfile)
            mywriter.writerow(['BLK'])
            for klb in new_blk:
                mywriter.writerow(klb)


scrapeing_cat()
